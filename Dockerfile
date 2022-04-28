FROM python:3.8.8
ENV PROJECTS_DIR=/opt/spider
COPY . $PROJECTS_DIR
COPY ./entrypoint.sh /
RUN pip install -r $PROJECTS_DIR/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
VOLUME ["$PROJECTS_DIR/area_code", "$PROJECTS_DIR/result"]
WORKDIR $PROJECTS_DIR
ENTRYPOINT ["/entrypoint.sh"]