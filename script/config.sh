
host=$1
is_secure=$2

CM_USER="admin"
CM_PASS="admin"


if [ "$host" != "" ]; then
echo "HOST  IS : $host #######"
  CM_URL="http://$host:7180"
  INSECURE=""

  if [ $is_secure == 1 ]; then
    CM_URL="https://$HOST:7183"
    INSECURE=" --insecure"
  fi

  VERSION=`curl -u $CM_USER:$CM_PASS "$CM_URL/api/version" $INSECURE`
  echo "API Version is: $VERSION"

  API_URL="$CM_URL/api/$VERSION"
  echo "API Url: $API_URL"
fi 

JAVA_HOME=`readlink -e /etc/alternatives/java | sed 's/\/jre\/bin\/java//g'`
CERT_DIR="/opt/cloudera/security/jks"
REMOTE_DIR="/tmp/certificate-install"

KEYSTORE_PASS="cloudera"
TRUSTSTORE_PASS="changeit"

