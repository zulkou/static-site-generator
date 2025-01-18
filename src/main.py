import os
import shutil

def copy_static(src, dst):
    if os.path.exists(dst):
        print(f"deleted \"{dst}\"")
        shutil.rmtree(dst)
    os.mkdir(dst)
    for path in os.listdir(src):
        src_path = os.path.join(src, path)
        dst_path = os.path.join(dst, path)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
            print(f"\"{src_path}\" copied into \"{dst_path}\"")
        else:
            print(f"created \"{dst_path}\" directory")
            copy_static(src_path, dst_path)
        

copy_static("static", "public")
