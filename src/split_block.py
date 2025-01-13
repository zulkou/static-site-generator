def markdown_to_blocks(markdown):
    doc = markdown.split("\n")
    result = []
    curr = ""
    for line in doc:
        stripped = line.strip()
        if not stripped:
            if curr:
                result.append(curr)
            curr = ""
        else:
            if curr:
                curr += "\n"
            curr += stripped
    if curr:
        result.append(curr)

    return result
