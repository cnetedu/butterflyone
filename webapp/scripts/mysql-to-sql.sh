#!/usr/bin/env bash

mysqldump --compact --compatible=ansi --default-character-set=binary mydbname |
grep -v ' KEY "' |
grep -v ' UNIQUE KEY "' |
perl -e 'local $/;$_=<>;s/,\n\)/\n\)/gs;print "begin;\n";print;print "commit;\n"' |
perl -pe '
if (/^(INSERT.+?)\(/) {
$a=$1;
s/\\'\''/'\'\''/g;
s/\\n/\n/g;
s/\),\(/\);\n$a\(/g;
}
' |
sqlite3 output.db
