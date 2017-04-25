<OPENSSL=${OPENSSL:-openssl}

COUNT=${COUNT:-1}
NPROCS=${NPROC:-$(getconf _NPROCESSORS_ONLN)}

makecert() {
  name=$1

  $OPENSSL genrsa -out ${name}.key 2048
  $OPENSSL req -new -key ${name}.key -out ${name}.csr \
    -subj /C=US/ST=CA/L=Norm/O=YLU/OU=Test/CN=${name}.com
  $OPENSSL x509 -req -days 365 \
    -in ${name}.csr -signkey ${name}.key -out ${name}.crt
  cat ${name}.crt ${name}.key > ${name}.pem
  rm -rf ${name}.csr ${name}.key ${name}.crt
}

for (( i = 0 ; i < $COUNT ; i += $NPROCS )); do
  for ((j = i; j < (i + $NPROCS) && j < $COUNT; j++ )) ; do
    makecert "test${j}" &
  done
  wait
  for ((j = i; j < (i + $NPROCS) && j < $COUNT; j++ )) ; do
    echo ssl_cert_name=test$i.pem
  done >> ssl_multicert.config
done
