#!/bin/bash
# ENX-Kebord Clean Reinstall Script

echo "🔄 ENX-Kebord Clean Reinstall"
echo "============================="
echo ""

# Uninstall first
echo "1️⃣ Removing existing installation..."
./uninstall.sh

echo ""
echo "2️⃣ Installing fresh version..."
./install.sh

echo ""
echo "✅ Clean reinstall completed!"
echo ""
echo "🚀 Launch with: enx-kebord"