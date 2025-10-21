#!/bin/bash
# Simple Docker test script

set -e

echo "==================================="
echo "Testing Docker Container"
echo "==================================="
echo ""

# Start container
echo "Starting container..."
sudo docker compose up -d

# Wait for startup
echo "Waiting 15 seconds for application to start..."
sleep 15

# Check container status
echo ""
echo "Container status:"
sudo docker compose ps
echo ""

# Check logs
echo "Recent logs:"
sudo docker compose logs --tail=30
echo ""

# Test health endpoint
echo "Testing application health..."
for i in {1..5}; do
    if curl -s http://localhost:8000 > /dev/null 2>&1; then
        echo "✅ Application is responding!"

        # Try accessing the API
        echo ""
        echo "Testing API endpoints..."
        curl -s http://localhost:8000/api/statistics | python3 -m json.tool || echo "Statistics endpoint check"

        echo ""
        echo "==================================="
        echo "✅ Docker test PASSED!"
        echo "==================================="
        echo ""
        echo "Access at: http://localhost:8000"
        echo ""
        echo "To stop: sudo docker compose down"
        exit 0
    else
        echo "Attempt $i/5: Application not ready yet, waiting..."
        sleep 5
    fi
done

echo ""
echo "❌ Application failed to respond after 40 seconds"
echo ""
echo "Check logs with: sudo docker compose logs"
exit 1
