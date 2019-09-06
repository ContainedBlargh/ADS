from argparse import ArgumentParser
from sys import argv
import requests
from zipfile import ZipFile
from io import BytesIO
from os import scandir, mkdir, walk
from os.path import isdir, basename
from shutil import copytree, make_archive, rmtree

parser = ArgumentParser(description='Downloads and distributes assignment submissions to teaching assistents.')
parser.add_argument('path', type=str, help='The path to the assignment zip.')
parser.add_argument('destination', type=str, help='The path to a folder that will be made by this process and filled with the assignments')
parser.add_argument('names', metavar='names', type=str, nargs='+', help='The names of the TAs (ie. "jvoi, khjo")')
parser.add_argument('-z', action="store_true", help='If set, the resulting folder is zipped as well.')

def unzip(zip_path):
    with ZipFile(zip_path) as z:
        name = str(basename(zip_path)).split('.')[0]
        dir_path = "./{}".format(name)
        z.extractall(path=dir_path)
        return dir_path

def collapse_prefixes_to_groups(dirs):
    assigned = set()
    groups = [[dirs[0].name]]
    assigned.add(0)
    for i, d in enumerate(dirs):
        if i in assigned:
            continue
        for g in groups:
            disc = str(g[0]).index('-', 0)
            if g[0][0:disc] == d.name[0:disc]:
                g.append(d.name)
                assigned.add(i)
        if i not in assigned:
            groups.append([d.name])
    return groups

def divide_assignments(dir_path, names, dest_path):
    n = len(names)
    batches = list(map(lambda i: [], range(n)))
    dirs = [d for d in scandir(dir_path)]
    print("Dividing {} submissions in a randomized order between {} TAs...".format(len(dirs), n))
    groups = collapse_prefixes_to_groups(dirs)
    for i, g in enumerate(groups):
        for member in g:
            batches[i%n].append(member)
    print("Copying files...")
    if not isdir(dest_path):
        mkdir(dest_path)
    for i, name in enumerate(names):
        name_dir = "./{}/{}".format(dest_path, name)
        if not isdir(name_dir):
            mkdir(name_dir)
        for f in batches[i]:
            fdest = "./{}/{}/{}".format(dest_path, name, f) 
            if not isdir(fdest):
                copytree("./{}/{}".format(dir_path, f), fdest)
    
def main(args):
    dir_path = unzip(args.path)
    divide_assignments(dir_path, args.names, args.destination)
    if args.z:
        print("Zipping to archive '{}'.zip".format(args.destination))
        make_archive(args.destination, 'zip', args.destination)
        rmtree(args.destination, ignore_errors=True)
    print("Done!")

if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
    pass
