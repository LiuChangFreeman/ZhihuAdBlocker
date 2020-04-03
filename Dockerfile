FROM centos/systemd
COPY mitm.service /etc/systemd/system/mitm.service
COPY block_zhihu_ad.py /home/block_zhihu_ad.py
COPY init.sh /home/init.sh
RUN yum -y install python3
RUN python3 -m pip install mitmproxy -i https://mirrors.aliyun.com/pypi/simple/
RUN chmod 777 /home/init.sh
RUN sh /home/init.sh
EXPOSE 8889
CMD ["/usr/sbin/init"]