import os
import sys
from argparse import ArgumentParser
from quarto import render


def md_with_list_of_htmls_in_dir(dir_path: str, level: int=2) -> str:
    """Creates Markdown string with list of html files in directory (recursive).
    List items work as links and are organized according to directory structure
    using headers of different levels.

    Args:
        dir_path (str): Path of directory to process.
        level (int, optional): Which level should be the header with dir name. 
            Defaults to 2.

    Returns:
        str: Formatted md output
    """
    dir_name = dir_path.split("/")[-1]
    contents = os.listdir(dir_path)

    header = f"\n\n{'#' * level} {str_to_human(dir_name)}\n\n"
    body = ""

    for item in contents:
        item_path = f"{dir_path}/{item}"
        if os.path.isdir(item_path):
            body += md_with_list_of_htmls_in_dir(item_path, level=level+1)
        else:
            file_name, file_type = os.path.splitext(item)
            if file_type in [".html", ".md"]: 
                body += f"- [{str_to_human(file_name)}]({item_path})\n"

    if not body:
        return body
    
    result = header + body
    return result


def str_to_human(x: str) -> str:
    """Takes string as is usually used in filenames or code 
    (lowercase, words separated by underscore etc.) 
    and transforms it to how humans would write it 
    (spaces, capital letters)"""
    res = (
        x
        .replace("-", "_")
        .split("_")
    )
    res = [word.capitalize() for word in res]
    
    return " ".join(res)


def save_md_str(md_input: str, output_path: str):
    assert os.path.splitext(output_path)[-1] == ".md"
    with open(output_path, "w") as file:
        file.write(md_input)


def convert_md_to_html(md_file: str, html_file: str):
    render(input=md_file, output_format="html", output_file=html_file)


def main(input_dir_path: str, output_path: str = "index.html"):
    """Create html file with links to htmls in directory.

    Args:
        input_dir_path (str, optional): Path to directory to process. 
        output_path (str, optional): Path to resulting html. Defaults to "index.html".
    """
    contents = md_with_list_of_htmls_in_dir(input_dir_path)
    md_path = output_path.replace(".html", ".md")
    save_md_str(contents, md_path)
    convert_md_to_html(md_path, output_path)
    # convert_md_to_html(contents, output_path)
    os.remove(md_path)


if __name__ == "__main__":
    parser = ArgumentParser(description='Create html file with links to htmls in directory.')
    parser.add_argument("input_dir_path", type=str, help="Path to directory to process")
    parser.add_argument("output_path", type=str, help="Path to resulting html")
    args = parser.parse_args()

    main(args.input_dir_path, args.output_path)
