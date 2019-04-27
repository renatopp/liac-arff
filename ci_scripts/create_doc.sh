set -euo pipefail

# Check if DOCPUSH is set
if ! [[ -z ${DOCPUSH+x} ]]; then

    if [[ "$DOCPUSH" == "true" ]]; then

        # install documentation building dependencies
        pip install sphinx sphinx-gallery sphinx_bootstrap_theme
        # $1 is the branch name
        # $2 is the global variable where we set the script status

        if ! { [ $1 = "master" ]; }; then
            { echo "Not one of the allowed branches"; exit 0; }
        fi

        # create the documentation
        cd docs && make html

        # takes a variable name as an argument and assigns the script outcome to a
        # variable with the given name. If it got this far, the script was successful
        function set_return() {
            # $1 is the variable where we save the script outcome
            local __result=$1
            local  status='success'
            eval $__result="'$status'"
        }

        set_return "$2"
    fi
fi
# Workaround for travis failure
set +u