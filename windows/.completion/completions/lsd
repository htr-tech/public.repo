_lsd() {
    local i cur prev opts cmds
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    cmd=""
    opts=""

    for i in ${COMP_WORDS[@]}
    do
        case "${i}" in
            lsd)
                cmd="lsd"
                ;;
            
            *)
                ;;
        esac
    done

    case "${cmd}" in
        lsd)
            opts=" -a -A -F -l -1 -R -h -d -t -S -X -v -U -r -i -L -Z -V -I  --all --almost-all --classify --long --ignore-config --oneline --recursive --human-readable --tree --directory-only --total-size --timesort --sizesort --extensionsort --versionsort --no-sort --reverse --group-directories-first --classic --no-symlink --inode --dereference --context --header --help --version --color --icon --icon-theme --config-file --depth --permission --size --date --sort --group-dirs --blocks --ignore-glob --hyperlink  <FILE>... "
            if [[ ${cur} == -* || ${COMP_CWORD} -eq 1 ]] ; then
                COMPREPLY=( $(compgen -W "${opts}" -- "${cur}") )
                return 0
            fi
            case "${prev}" in
                
                --color)
                    COMPREPLY=($(compgen -W "always auto never" -- "${cur}"))
                    return 0
                    ;;
                --icon)
                    COMPREPLY=($(compgen -W "always auto never" -- "${cur}"))
                    return 0
                    ;;
                --icon-theme)
                    COMPREPLY=($(compgen -W "fancy unicode" -- "${cur}"))
                    return 0
                    ;;
                --config-file)
                    COMPREPLY=($(compgen -f "${cur}"))
                    return 0
                    ;;
                --depth)
                    COMPREPLY=($(compgen -f "${cur}"))
                    return 0
                    ;;
                --permission)
                    COMPREPLY=($(compgen -W "rwx octal" -- "${cur}"))
                    return 0
                    ;;
                --size)
                    COMPREPLY=($(compgen -W "default short bytes" -- "${cur}"))
                    return 0
                    ;;
                --date)
                    COMPREPLY=($(compgen -f "${cur}"))
                    return 0
                    ;;
                --sort)
                    COMPREPLY=($(compgen -W "size time version extension none" -- "${cur}"))
                    return 0
                    ;;
                --group-dirs)
                    COMPREPLY=($(compgen -W "none first last" -- "${cur}"))
                    return 0
                    ;;
                --blocks)
                    COMPREPLY=($(compgen -W "permission user group context size date name inode links" -- "${cur}"))
                    return 0
                    ;;
                --ignore-glob)
                    COMPREPLY=($(compgen -f "${cur}"))
                    return 0
                    ;;
                    -I)
                    COMPREPLY=($(compgen -f "${cur}"))
                    return 0
                    ;;
                --hyperlink)
                    COMPREPLY=($(compgen -W "always auto never" -- "${cur}"))
                    return 0
                    ;;
                *)
                    COMPREPLY=()
                    ;;
            esac
            COMPREPLY=( $(compgen -W "${opts}" -- "${cur}") )
            return 0
            ;;
        
    esac
}

complete -F _lsd -o bashdefault -o default lsd
