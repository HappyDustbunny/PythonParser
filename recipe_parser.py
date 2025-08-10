import os

def main():
    chunk = []
    all_text = []
    my_file = os.path.join('.', 'SbSCookbook')  # Put the translation here. REMEMBER to precede lines containing ()
                                                # with a * and remove the star manually

    with open(my_file, encoding='utf8') as in_file, \
        open("output_file.html", "a", encoding='utf8') as out_file:
        read_file = in_file.readlines()

        for line in read_file:  # The text is read into a buffer (the variable chunk). When a trigger is reached, the
                                # chunk is processed and the process repeated
            if line:
                chunk.append(line)
            if line[0] == '(' and line[-2] == ')':
                all_text = wrap_name(chunk, all_text)
                chunk = []
                if line.strip():
                    chunk.append(line)
            elif line.strip() == 'Method:':
                all_text = wrap_ingredients(chunk, all_text)
                chunk = []
                if line.strip():
                    chunk.append(line)
            elif line.strip() == 'End':  # REMEMBER to remove () here
                all_text = wrap_method(chunk, all_text)

        for line in all_text:
            out_file.writelines(line)
        
    print("Over and out")


def wrap_name(chunk, all_text):
    all_text.append('<button class="recipe">\n')
    all_text.append('\t<h3> ' + chunk[0].strip() + ' </h3>\n')
    all_text.append('</button>\n\n')
    return all_text


def wrap_ingredients(chunk, all_text):
    all_text.append('<div class="ingredienser">')
    all_text.append('<p class="antal"> ' + chunk[0].strip() + ' </p>\n')
    all_text.append('<b> Ingredients: </b>\n')
    for line in chunk:
        if line[0] == '(' and line[-2] == ')' or line == '\n':
            pass
        else:
            all_text.append('\t<p><label><input type="checkbox"> ' + line.strip() + ' </label></p>\n')

    all_text.append('</div>\n')
    return all_text


def wrap_method(chunk, all_text):
    all_text.append('<div class="howto"> <b> Method: </b>\n')
    for line in chunk:
        if line.strip() == 'Method:' or line == '\n':
            pass
        else:
            all_text.append('\t<p><label><input type="checkbox">' + line.strip() + '</label></p>\n')

    all_text.append('\t<button class="slut">(End)</button>')
    all_text.append('</div>\n')
    return all_text

if __name__ == '__main__':
    main()
