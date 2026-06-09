def extract_title(markdown):
    with open(markdown) as f:
        first = f.readline()
        if first.startswith("#"):
            return first[2:].strip()
        else:
            raise Exception("No h1 found in the markdown file")
