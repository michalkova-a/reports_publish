import os
from argparse import ArgumentParser


def html_with_list_of_htmls_in_dir(dir_path: str, level: int=2) -> str:
    """Creates HTML string with list of html files in directory (recursive).
    List items work as links and are organized according to directory structure
    using headers of different levels.

    Args:
        dir_path (str): Path of directory to process.
        level (int, optional): Which level should be the header with dir name. 
            Defaults to 2.

    Returns:
        str: Formatted HTML output
    """
    dir_name = dir_path.split("/")[-1]
    contents = os.listdir(dir_path)

    header = f"\n\n<h{level}> {str_to_human(dir_name)}</h{level}>\n\n"
    body = ""

    # files first
    for item in contents:
        item_path = os.path.join(dir_path, item)
        if os.path.isfile(item_path):
            file_name, file_type = os.path.splitext(item)
            if file_type == ".html": 
                body += f"<li><a href='{item_path}'>{str_to_human(file_name)}</a></li>\n"

    # wrap list items to <ul></ul> (if there's something to wrap)
    if body:
        body = f"<ul>\n{body}</ul>\n\n"

    # then subdirectories
    for item in contents:
        item_path = os.path.join(dir_path, item)
        if os.path.isdir(item_path):
            body += html_with_list_of_htmls_in_dir(item_path, level=level+1)

    # don't print headers for directories which have nothing to be added to the list
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


def wrap_html_str(html_input: str, css_path: str = "styles/bootstrap.css", title: str = "Index") -> str:
    """HTML string is wrapped inside <body></body>,
    header with CSS style is added. 

    Args:
        html_input (str): Body of the page formatted using HTML.

    Returns:
        str: Full HTML page content with CSS styles.
    """
    output = (
        f"<!doctype html>\n"
        f"<html>\n"
        f"<head>\n"
        f"  <meta charset='utf-8'>\n"
        f"  <meta name='viewport' content='width=device-width, initial-scale=1'>\n"
        f"  <title>{title}</title>\n"
        f"  <link rel='stylesheet' href='{css_path}'>\n"
        f"</head>\n"
        f"<body>\n"
        f"{html_input}\n"
        f"</body>\n"
        f"</html>"
    )
    return output


def save_html_str(html_input: str, output_path: str):
    assert os.path.splitext(output_path)[-1] == ".html"
    with open(output_path, "w") as file:
        file.write(html_input)


def main(input_dir_path: str, output_path: str = "index.html"):
    """Create html file with links to htmls in directory.

    Args:
        input_dir_path (str, optional): Path to directory to process. 
        output_path (str, optional): Path to resulting html. Defaults to "index.html".
    """
    contents = html_with_list_of_htmls_in_dir(input_dir_path)
    contents = wrap_html_str(contents)
    save_html_str(contents, output_path)


if __name__ == "__main__":
    parser = ArgumentParser(description='Create html file with links to htmls in directory.')
    parser.add_argument("input_dir_path", type=str, help="Path to directory to process")
    parser.add_argument("output_path", type=str, help="Path to resulting html")
    args = parser.parse_args()

    main(args.input_dir_path, args.output_path)
