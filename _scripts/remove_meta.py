import glob
import re

files = glob.glob('*.html')
for file in files:
    print("File: %s" % file)
    in_removal = False
    new_content = []
    lines = open(file, 'r', encoding='utf8').readlines()
    with open(file, 'w', encoding='utf8') as new_file:
        for line in lines:
            if line.startswith('meta:'):
                in_removal = True
                continue
            elif line.startswith('---'):
                in_removal = False
            elif in_removal:
                continue
            if 'pre' in line:
                tmp = re.sub(r'<pre.*?lang="(.*?)".*?>', '\n{% highlight \\1 %}\n', line)
                tmp2 = re.sub(r'<pre.*?>', '\n{% highlight %}\n', tmp)
                new_line = re.sub(r'</pre>', '\n{% endhighlight %}\n', tmp2)
                print("new_line: %s" % new_line)
            else:
                new_line = line

            new_file.write(new_line)
