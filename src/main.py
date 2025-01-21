import os
import shutil
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
    with open(from_path) as src, open(template_path) as tmplt:
        source = src.read()
        template = tmplt.read()
        
        content = markdown_to_html_node(source)
        print(f"Type of content: {type(content)}")  # Add this debug line
        html_content = content.to_html()

        title = extract_title(source)

        # Replace both placeholders in the template
        final_html = template.replace("{{ Title }}", title)
        final_html = final_html.replace("{{ Content }}", html_content)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as dest:
        dest.write(final_html)

copy_static("static", "public")
generate_page("content/index.md", "template.html", "public/index.html")
