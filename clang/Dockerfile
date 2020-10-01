FROM nvidia/cuda:9.2-base
ADD . /clang/
WORKDIR /clang/llvm-project/build
RUN apt-get update && apt-get install -y cmake g++ python && \
cmake -DLLVM_ENABLE_PROJECTS=clang -DBUILD_SHARED_LIBS=ON -G "Unix Makefiles" \
 -DCMAKE_BUILD_TYPE=Release \
 ../llvm && \
make -j8  && \
cmake -DCMAKE_INSTALL_PREFIX=/clang/install -P cmake_install.cmake && make clean
#MKDIR build
#WORKDIR build
