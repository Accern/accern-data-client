
REGEX="^v(0|[1-9][0-9]*)$$"
CUR_VERSION=$(git describe --tags --abbrev=0)

# SAMPLES
# "v1.0.0rc2"
# "v1.0.0"
# "v0.1.0rc2"
# "v0.1.0"
# "v0.1.1rc2"
# "v0.1.1"

echo "Current version is: ${CUR_VERSION}"
MAJOR_VERSION=$(echo "${CUR_VERSION}" | awk -F'rc' '{print $1}' | awk -F'v' '{print $2}' | awk -F'.' '{print $1}')
MINOR_VERSION=$(echo "${CUR_VERSION}" | awk -F'rc' '{print $1}' | awk -F'v' '{print $2}' | awk -F'.' '{print $2}')
PATCH_VERSION=$(echo "${CUR_VERSION}" | awk -F'rc' '{print $1}' | awk -F'v' '{print $2}' | awk -F'.' '{print $3}')
RC_VERSION=$(echo "${CUR_VERSION}" | awk -F'rc' '{print $2}')

PS3='Please enter your choice: '
options=(
    "Added new functionality while breaking the existing code."
    "Added new functionality without breaking the existing code."
    "Bug fix"
    "Stable release")
select opt in "${options[@]}"
do
    case $opt in
        ${options[0]})
            if [ $MAJOR_VERSION -ne 0 ] && [ $MINOR_VERSION -eq 0 ] && [ $PATCH_VERSION -eq 0 ] && [ $RC_VERSION ] && [ $RC_VERSION -ne 0 ]
            then
                RC_VERSION=$((RC_VERSION + 1))
            else
                MAJOR_VERSION=$((MAJOR_VERSION + 1))
                MINOR_VERSION=0
                PATCH_VERSION=0
                RC_VERSION=1
            fi
            break
            ;;
        ${options[1]})
            if [ $MINOR_VERSION -ne 0 ] && [ $PATCH_VERSION -eq 0 ] && [ $RC_VERSION ] && [ $RC_VERSION -ne 0 ]
            then
                RC_VERSION=$((RC_VERSION + 1))
            else
                MINOR_VERSION=$((MINOR_VERSION + 1))
                PATCH_VERSION=0
                RC_VERSION=1
            fi
            break
            ;;
        ${options[2]})
            if [ $PATCH_VERSION -ne 0 ] && [ $RC_VERSION ] && [ $RC_VERSION -ne 0 ]
            then
                RC_VERSION=$((RC_VERSION + 1))
            else
                PATCH_VERSION=$((PATCH_VERSION + 1))
                RC_VERSION=1
            fi
            break
            ;;
        ${options[3]})
            if ! [ $RC_VERSION ]
            then
                echo "Already a stable release." || exit 0
            fi
            RC_VERSION=0
            break
            ;;
        *) echo "Invalid option $REPLY";;
    esac
done

if [ -n $RC_VERSION -a $RC_VERSION -ne 0 ]
then
    echo "v${MAJOR_VERSION}.${MINOR_VERSION}.${PATCH_VERSION}rc${RC_VERSION}"
else
    echo "v${MAJOR_VERSION}.${MINOR_VERSION}.${PATCH_VERSION}"
fi
