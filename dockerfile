FROM python:3.9

WORKDIR /usr/src/app
COPY . .

RUN apt-get update 

RUN    apt-get install --assume-yes --no-install-recommends --quiet \
	software-properties-common  

RUN apt-get -y install libc-dev
RUN apt-get -y install build-essential
RUN pip install -U pip

RUN  apt-get install apt-utils -y 

RUN  add-apt-repository -y ppa:deadsnakes/ppa 
RUN  apt install --assume-yes  python3  -y &&  apt install python3-pip -y

RUN  pip3 --default-timeout=600 install --no-cache-dir -r requirements.txt

run pip3 install numpy

CMD ["python", "./coco_json_to_csv.py", "http://images.cocodataset.org/annotations/annotations_trainval2017.zip", "/home/"]

