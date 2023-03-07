echo "Deploying to cluster" \
    && kubectl cp build/_app default/static-fc754b8cf-x5lsw:/usr/share/nginx/html/ \
    && kubectl cp build/index.html default/static-fc754b8cf-x5lsw:/usr/share/nginx/html/ \
    && kubectl cp build/favicon.ico default/static-fc754b8cf-x5lsw:/usr/share/nginx/html/ \
    && kubectl cp build/robots.txt default/static-fc754b8cf-x5lsw:/usr/share/nginx/html/ \
    && echo "Copied build files to cluster"