echo noop | sudo tee /sys/block/sdb/queue/scheduler

cd bin/Release

echo 3 | sudo tee /proc/sys/vm/drop_caches
sudo ./Measurements.exe 1TB /dev/sdb

echo 3 | sudo tee /proc/sys/vm/drop_caches
sudo ./Measurements.exe 1GB /dev/sdb

echo 3 | sudo tee /proc/sys/vm/drop_caches
sudo ./Measurements.exe 128MB /dev/sdb

echo 3 | sudo tee /proc/sys/vm/drop_caches
sudo ./Measurements.exe 16MB /dev/sdb

