import subprocess
import os
import math
import logzero

logger = logzero.logger

MAX_SPLIT_SIZE = 4024

def file_split_7z(file_path, split_size=MAX_SPLIT_SIZE):
    file_path_7z_list = []
    # if origin file is 7z file rename it
    origin_file_path = ""
    if os.path.splitext(file_path)[1] == ".7z":
        origin_file_path = file_path
        file_path = os.path.splitext(origin_file_path)[0] + ".7zo"
        os.rename(origin_file_path, file_path)
    # do 7z compress
    fz = os.path.getsize(file_path) / 1024 / 1024
    pa = math.ceil(fz / split_size)
    head, ext = os.path.splitext(os.path.abspath(file_path))
    archive_head = "".join((head, ext.replace(".", "_"))) + ".7z"
    for i in range(pa):
        check_file_name = "{}.{:03d}".format(archive_head, i + 1)
        if os.path.isfile(check_file_name):
            logger.debug("remove exists file | {}".format(check_file_name))
            os.remove(check_file_name)
    cmd_7z = ["7z", "a", "-v{}m".format(split_size), "-y", "-mx0", archive_head, file_path]
    proc = subprocess.Popen(cmd_7z, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    if b"Everything is Ok" not in out:
        logger.error("7z output | {}".format(out.decode("utf-8")))
        logger.error("7z error | {}".format(err.decode("utf-8")))
        return file_path_7z_list

    for i in range(pa):
        file_path_7z_list.append("{}.{:03d}".format(archive_head, i + 1))
    # if origin file is 7z file rename it back
    if origin_file_path:
        os.rename(file_path, origin_file_path)
    return file_path_7z_list

def do_file_split(file_path, split_size=MAX_SPLIT_SIZE):
    """caculate split size
        example max split size is 1495 file size is 2000
            than the split part num should be int(2000 / 1495 + 0.5) = 2
            so the split size should be 1000 + 1000 but not 1495 + 505
            with the file size increase the upload risk would be increase too
         """

    file_size = os.path.getsize(file_path) / 2 ** 20
    split_part = math.ceil(file_size / split_size)
    new_split_size = math.ceil(file_size / split_part)
    logger.info("file size | {} | split num | {} | split size | {}".format(file_size, split_part, new_split_size))
    file_path_7z_list = file_split_7z(file_path, split_size=new_split_size)
    return file_path_7z_list

def __copyInFile(iF, oF, buffersize=1024, tocopy = 0):
    copied = 0
    i = 0
    while True:
        i += 1
        elsetocpy = tocopy - copied
        # free to copy all
        if (elsetocpy - buffersize > 0) or (tocopy == 0):
            tmp = iF.read(buffersize)
            if tmp == b'':
                if i == 1:
                    return False
                else:
                    return True
            else:
                oF.write(tmp)
                copied += buffersize
        # last data to copy
        else:
            tmp = iF.read(elsetocpy)
            if tmp == b'':
                if i == 1:
                    return False
                else:
                    return True
            else:
                oF.write(tmp)
                return True

def split(inFileSrc, output, splitIn):
    splitNumber = 1
    try:
        inFile = open(inFileSrc, 'rb');
    except FileNotFoundError:
        print('Error: the file %s does not exists. Exiting...' % (inFileSrc))
        exit()
    while True:
        if output == None:
            outFile = open(inFileSrc + '.' + str('%03d' % (splitNumber)), 'wb')
        else:
            outFile = open(os.path.join(output, os.path.basename(inFileSrc)) + '.' + str('%03d' % (splitNumber)), 'wb')
        if not __copyInFile(inFile, outFile, 1024, splitIn):
            outFile.close()
            if output == None:
                os.remove(inFileSrc + '.' + str('%03d' % (splitNumber)))
            else:
                os.remove(os.path.join(output, os.path.basename(inFileSrc)) + '.' + str('%03d' % (splitNumber)))
            break
        else:
            outFile.close()
            splitNumber += 1
def getUnitAndValue(inVar):
    inVar = str(inVar)
    number = ''
    unit = ''
    for l in inVar:
        if(l.isdigit() or l == ',' or l == '.'):
            if l == ',':
                l = '.'
            number += l
        else:
            unit += l
    number = float(number)
    return (number, unit)

def getBytes(inVar):
    tmp = getUnitAndValue(inVar)
    number = tmp[0]
    unit = tmp[1]
    del tmp
    #IS
    print(unit)
    if(unit == 'k' or unit == 'K' or unit == 'KB'):
        return int(number * 1000)
    elif(unit == 'm' or unit == 'M' or unit == 'MB'):
        return int(number * 1000000)
    elif(unit == 'g' or unit == 'G' or unit == 'GB'):
        return int(number * 1000000000)
    elif(unit == 't' or unit == 'T' or unit == 'TB'):
        return int(number * 1000000000000)
    elif(unit == 'p' or unit == 'P' or unit == 'PB'):
        return int(number * 1000000000000000)
    elif(unit == 'e' or unit == 'E' or unit == 'EB'):
        return int(number * 1000000000000000000)
    elif(unit == 'z' or unit == 'Z' or unit == 'ZB'):
        return int(number * 1000000000000000000000)
    elif(unit == 'y' or unit == 'Y' or unit == 'YB'):
        return int(number * 1000000000000000000000000)
    #BU
    elif(unit == 'KiB'):
        return int(number * 1024)
    elif(unit == 'MiB'):
        return int(number * 1048576)
    elif(unit == 'GiB'):
        return int(number * 1073741824)
    elif(unit == 'TiB'):
        return int(number * 1099511627776)
    elif(unit == 'PiB'):
        return int(number * 1125899906842624)
    elif(unit == 'EiB'):
        return int(number * 1152921504606846976)
    elif(unit == 'ZiB'):
        return int(number * 1180591620717411303424)
    elif(unit == 'YiB'):
        return int(number * 1208925819614629174706176)
    elif(unit == '' or unit == 'b' or unit == 'B'):
        return int(number)
    else:
        print('Fatal error during conversion of %s, is an effective unit of measure? Exiting...' % (str(inVar)))
        exit()

#nameFile = "Free Guy (2021) Lat-Eng 1080 @StreamingLatino.mp4"
#split(f'./download/{nameFile}', './', getBytes('2000.0MB'))