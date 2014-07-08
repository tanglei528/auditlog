DOC_PATH=/usr/share/doc/%{name}-%{unmangled_version}

[ -d /etc/auditlog/ ] || mkdir /etc/auditlog
[ -d /var/log/auditlog/ ] || mkdir /var/log/auditlog
[ -d /var/run/auditlog/ ] || mkdir /var/run/auditlog
[ -d /usr/share/man/man1 ] || mkdir -p /usr/share/man/man1
[ -f /etc/auditlog/auditlog.conf ] || cp ${DOC_PATH}/auditlog.conf /etc/auditlog/
[ -f /etc/auditlog/policy.json ] || cp ${DOC_PATH}/policy.json /etc/auditlog/
[ -f /etc/init.d/auditlog-api ] || cp ${DOC_PATH}/auditlog-api /etc/init.d/
if [ ! -f /usr/share/man/man1/auditlog.1.gz ]; then
   cp ${DOC_PATH}/auditlog.1 /usr/share/man/man1
   gzip /usr/share/man/man1/auditlog.1
fi
chmod +x /etc/init.d/auditlog-api
chkconfig --add auditlog-api
