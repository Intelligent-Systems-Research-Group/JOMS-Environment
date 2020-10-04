FROM nvidia/cuda:9.2-base
ADD . /clang/
WORKDIR /clang
RUN apt-get update && apt-get install -y g++ python wget build-essential git
RUN git clone https://github.com/llvm/llvm-project
RUN wget https://github.com/Kitware/CMake/releases/download/v3.18.3/cmake-3.18.3-Linux-x86_64.sh
RUN chmod +x cmake-3.18.3-Linux-x86_64.sh && printf 'y\n' > params && ./cmake-3.18.3-Linux-x86_64.sh < "params" 
WORKDIR /clang/llvm-project
RUN git checkout origin/release/7.x
WORKDIR /clang/llvm-project/build
RUN /clang/cmake-3.18.3-Linux-x86_64/bin/cmake -DLLVM_ENABLE_PROJECTS=clang -DBUILD_SHARED_LIBS=ON -G "Unix Makefiles" \
 -DCMAKE_BUILD_TYPE=Release \
 ../llvm && \
make -j8  && \
/clang/cmake-3.18.3-Linux-x86_64/bin/cmake -DCMAKE_INSTALL_PREFIX=/clang/install -P cmake_install.cmake && make clean
RUN /clang/install/bin/clang++ -v
#MKDIR build
#WORKDIR build
