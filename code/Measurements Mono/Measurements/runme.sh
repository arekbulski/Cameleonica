echo noop | sudo tee /sys/block/sdb/queue/scheduler

cd bin/Release

echo 3 | sudo tee /proc/sys/vm/drop_caches
sudo ./Measurements.exe 1TB /dev/sdb

echo 3 | sudo tee /proc/sys/vm/drop_caches
sudo ./Measurements.exe 512GB /dev/sdb

echo 3 | sudo tee /proc/sys/vm/drop_caches
sudo ./Measurements.exe 256GB /dev/sdb

echo 3 | sudo tee /proc/sys/vm/drop_caches
sudo ./Measurements.exe 128GB /dev/sdb

echo 3 | sudo tee /proc/sys/vm/drop_caches
sudo ./Measurements.exe 64GB /dev/sdb

echo 3 | sudo tee /proc/sys/vm/drop_caches
sudo ./Measurements.exe 32GB /dev/sdb

echo 3 | sudo tee /proc/sys/vm/drop_caches
sudo ./Measurements.exe 16GB /dev/sdb

echo 3 | sudo tee /proc/sys/vm/drop_caches
sudo ./Measurements.exe 8GB /dev/sdb

echo 3 | sudo tee /proc/sys/vm/drop_caches
sudo ./Measurements.exe 4GB /dev/sdb

echo 3 | sudo tee /proc/sys/vm/drop_caches
sudo ./Measurements.exe 2GB /dev/sdb

echo 3 | sudo tee /proc/sys/vm/drop_caches
sudo ./Measurements.exe 1GB /dev/sdb

echo 3 | sudo tee /proc/sys/vm/drop_caches
sudo ./Measurements.exe 512MB /dev/sdb

echo 3 | sudo tee /proc/sys/vm/drop_caches
sudo ./Measurements.exe 256MB /dev/sdb

echo 3 | sudo tee /proc/sys/vm/drop_caches
sudo ./Measurements.exe 128MB /dev/sdb

echo 3 | sudo tee /proc/sys/vm/drop_caches
sudo ./Measurements.exe 64MB /dev/sdb

echo 3 | sudo tee /proc/sys/vm/drop_caches
sudo ./Measurements.exe 32MB /dev/sdb

echo 3 | sudo tee /proc/sys/vm/drop_caches
sudo ./Measurements.exe 16MB /dev/sdb

echo 3 | sudo tee /proc/sys/vm/drop_caches
sudo ./Measurements.exe 8MB /dev/sdb

echo 3 | sudo tee /proc/sys/vm/drop_caches
sudo ./Measurements.exe 4MB /dev/sdb

echo 3 | sudo tee /proc/sys/vm/drop_caches
sudo ./Measurements.exe 2MB /dev/sdb

echo 3 | sudo tee /proc/sys/vm/drop_caches
sudo ./Measurements.exe 1MB /dev/sdb
