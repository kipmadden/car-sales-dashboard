#!/bin/bash

# CI/CD deployment script
# This script builds and deploys the application

set -e

echo "🚀 Starting deployment process..."

# Build Docker image
echo "🐳 Building Docker image..."
docker build -t car-sales-dashboard:latest .

# Run smoke tests
echo "🔍 Running smoke tests..."
docker run -d --name smoke-test -p 3000:3000 car-sales-dashboard:latest

# Wait for container to be ready
echo "⏳ Waiting for application to start..."
sleep 60

# Check container status
echo "📊 Checking container status..."
docker ps -a

# Test health endpoint
echo "🏥 Testing health endpoint..."
for i in {1..5}; do
    if curl -f http://localhost:3000/healthz; then
        echo "✅ Health check passed!"
        break
    else
        echo "❌ Health check attempt $i failed, waiting 10 seconds..."
        sleep 10
        if [ $i -eq 5 ]; then
            echo "❌ All health check attempts failed, showing container logs:"
            docker logs smoke-test
            docker stop smoke-test
            docker rm smoke-test
            exit 1
        fi
    fi
done

# Clean up smoke test
docker stop smoke-test
docker rm smoke-test

echo "✅ Deployment tests passed!"

# Tag image for deployment
if [ "$CI" = "true" ]; then
    echo "🏷️ Tagging image for registry..."
    docker tag car-sales-dashboard:latest ghcr.io/$GITHUB_REPOSITORY:latest
    docker tag car-sales-dashboard:latest ghcr.io/$GITHUB_REPOSITORY:$GITHUB_SHA
fi

echo "🎉 Deployment process complete!"
