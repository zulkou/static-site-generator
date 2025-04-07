import os
import shutil
from pathlib import Path
from split_block import extract_title, markdown_to_html_node

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

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from \"{from_path}\" to \"{dest_path}\" using \"{template_path}\"")
    with open(str(from_path)) as src, open(str(template_path)) as tmplt:
        source = src.read()
        template = tmplt.read()
        
        print(f"About to process markdown from {from_path}")
        try:
            content = markdown_to_html_node(source)
            html_content = content.to_html()
        except Exception as e:
            print(f"Error processing markdown in {from_path}")
            print(f"Error details: {str(e)}")
            raise

        title = extract_title(source)

        final_html = template.replace("{{ Title }}", title)
        final_html = final_html.replace("{{ Content }}", html_content)

    os.makedirs(os.path.dirname(str(dest_path)), exist_ok=True)

    with open(str(dest_path), "w") as dest:
        dest.write(final_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    src_dir = Path(dir_path_content)
    dst_dir = Path(dest_dir_path)

    for path in src_dir.iterdir():
        if path.is_dir():
            new_src = src_dir / path.name
            new_dst = dst_dir / path.name

            new_dst.mkdir(exist_ok=True, parents=True)
            generate_pages_recursive(new_src, template_path, new_dst)
        elif path.is_file():
            if path.suffix == ".md":
                dst_file = dst_dir / (path.stem + ".html")
                generate_page(path, template_path, dst_file)

def main():
    copy_static("static", "public")
    generate_pages_recursive("content", "template.html", "public")

if __name__ == "__main__":
    main()
