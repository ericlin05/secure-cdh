#!/bin/bash

set -e

SERVER_HOST="$1"
AGENT_HOST_STRING="$2"
TYPE="$3"

BASE_DIR=$(dirname $0)
source $BASE_DIR/../../config.sh

AGENT_HOSTS=(`echo $AGENT_HOST_STRING | sed 's/,/\n/g'`)

if [ $TYPE == '' ] || [ $TYPE != 'self' ] || [ $TYPE != 'ca' ]; then
  TYPE='self'
fi

run_on_host()
{
  host=$1
  is_cm=$2
  cert_type=$3
  echo ""
  echo "========================================================"
  echo "Running on host: $host"
  ssh root@$host "rm -fr $REMOTE_DIR; mkdir $REMOTE_DIR"
  echo ""
  echo "Copying files to remote host $host:$REMOTE_DIR"
  scp -r $BASE_DIR/../../* root@$host:$REMOTE_DIR

  echo ""
  echo "Running command: bash $REMOTE_DIR/ssl/cm/cert-gen.sh $is_cm $cert_type"
  ssh root@$host "bash $REMOTE_DIR/ssl/cm/cert-gen.sh $is_cm $cert_type" 

  echo ""
  echo "Cleaning up files"
  ssh root@$host "rm -fr $REMOTE_DIR"
  echo "========================================================"
}

run_on_host $SERVER_HOST "1" $TYPE
for host in "${AGENT_HOSTS[@]}"
do
  run_on_host $host "0" $TYPE
done

