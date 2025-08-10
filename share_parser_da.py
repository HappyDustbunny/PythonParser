import os
import re
import string


def main():
    flag = 'lowered'
    chunk = []
    all_text = []
    my_file = os.path.join('.', 'kogebog.html')

    with open(my_file, encoding='utf8') as in_file, \
            open("kogebog_output_file.html", "a", encoding='utf8') as out_file:
        read_file = in_file.readlines()

        for line in read_file:
            if re.search(r'<p class="antal">', line):
                dump_chunk_into_all_text(chunk, all_text)
                chunk = []  # Reset chunk
                all_text = wrap_serves(line, all_text)
            elif '"recipe"' in line:  # Lines with ID will not have the last "
                flag = 'raised'
                dump_chunk_into_all_text(chunk, all_text)
                chunk = []
            elif flag == 'raised':
                flag = 'raised_higher'
                all_text = wrap_add_id(line, all_text)
            elif flag == 'raised_higher':
                flag = 'lowered'
            elif line:
                chunk.append(line)

        for line in all_text:
            out_file.writelines(line)

    print("Over and out")


def wrap_serves(line, all_text):
    all_text.append('              <div class="recipeHeading">\n')
    all_text.append('                  ' + line.strip() + '\n')
    all_text.append('                  <button class="share">Del</button>\n')
    all_text.append('              </div>\n')
    return all_text


def wrap_add_id(line, all_text):
    recipe_id = re.sub('</?h3>', '', line, 2)
    recipe_id = re.sub('<span.+', '', recipe_id).strip()
    recipe_id = string.capwords(recipe_id)
    recipe_id = re.sub(' ', '', recipe_id, 50)
    recipe_id = re.sub('&AElig;', 'AE', recipe_id, 50)
    recipe_id = re.sub('&aelig;', 'ae', recipe_id, 50)
    recipe_id = re.sub('&aring;', 'aa', recipe_id, 50)
    recipe_id = re.sub('&oslash;', 'oe', recipe_id, 50)
    all_text.append('              <button ' + 'id="' + recipe_id + '" class="recipe">\n')
    all_text.append('                  ' + line.strip() + '\n')
    all_text.append('              </button>\n\n')
    return all_text


def dump_chunk_into_all_text(chunk, all_text):
    for line in chunk:
        all_text.append(line)
    return all_text


if __name__ == '__main__':
    main()
