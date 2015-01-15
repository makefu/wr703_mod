#!/usr/bin/python
""" usage: build [--size=<size>] [--bootloader=<path-to-loader>] [--openwrt=<path-to-image>] [--output=<path-to-file>] <full-dump>

Options:
    --size <size>                   the size of the new image [Default: 16m]
    --bootloader <path-to-loader>   path to the new bootloader [Default: uboot/bin/uboot_for_tp-link_tl-wr703n.bin]
    --output <path-to-file>         output file [Default: image.bin]
    --openwrt <path-to-image>       path to openwrt image, use factory image

full dump is essentially /dev/mtd5 on wr703

"""
from os.path import getsize
from docopt import docopt
from pprint import pprint
from humanfriendly import parse_size

args = docopt(__doc__)

# the block size
bs=parse_size('64k')

infile= args['<full-dump>']
outfile=args['--output']
bootloader=args['--bootloader']
openwrt_image=args['--openwrt']

new_size= parse_size(args['--size'])
orig_size=getsize(infile)
with open(outfile,'wb+') as out:
    with open(infile,'rb') as inf:
        # write the new bootloader
        print('writing bootloader at block 0')
        with open(bootloader,'rb') as bl:
            print('at position {} writing {} bytes'.format(out.tell(),out.write(bl.read())))
        # we now need to get the wr703 specifics, they are at 64k-128k
        print('writing hw specifics at block 1')
        inf.seek(bs)
        print('at position {} writing {} bytes'.format(out.tell(),out.write(inf.read(bs))))
        if openwrt_image:
            print('writing openwrt image')
            with open(openwrt_image,'rb') as owrt:
                print('at position {} writing {} bytes'.format(out.tell(),out.write(owrt.read())))
        else:
            print('no openwrt image given, skipping this step')
        print('writing empty space and art partition')
        inf.seek(orig_size-bs)
        print('skipping from position {} to position {}'.format(out.tell(),out.seek(new_size-bs)))

        print('at position {} writing {} bytes'.format(
            out.tell(),out.write(inf.read(bs))))
