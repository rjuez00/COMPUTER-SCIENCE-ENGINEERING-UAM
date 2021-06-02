more $1 | awk '
{
    if (NF==2) {
        if ($1 in n)
            print -1,$1; # already in hash
        else { # save in hash table
            n[$1]=$2;
            print $1;
        }

    } else if (NF==1) {
        if ($1 in n)
            print $1,n[$1];
        else
            print $1,-1;
    }
}' > $2
