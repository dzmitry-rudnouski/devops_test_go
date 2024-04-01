cd charts/go-app
helm dependency build
cd ..
helm upgrade --install go-app ./go-app
