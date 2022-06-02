# Android BLE Debuger

使用Android BLE工具连接测试CC2541 BLE

# 获取蓝牙地址

![0006_Use_Flash_Programmer_Read_IEEE.png](images/0006_Use_Flash_Programmer_Read_IEEE.png)

# Android BLE Debuger Install

* **BLE Scanner**比blecore更好用
* https://github.com/fszeng2011/blecore
* 华为手机可以直接在AppGallery检索安装：`BLE Debugger`  
  ![0006_BLECORE_Main_Page.jpg](images/0006_BLECORE_Main_Page.jpg)

# 使用方法

* 烧录：`C:\Texas Instruments\BLE-CC254x-1.4.2.2\Accessories\HexFiles\CC2541_SmartRF_SimpleBLEPeripheral.hex`
* 按下`S1`按键，启动程序，一定要按下这个按键，然后Android软件能够检测到设备；  
  ![0006_BLECORE_Detect_Device.jpg](images/0006_BLECORE_Detect_Device.jpg)
* 获取到的蓝牙广播：  
  ![0006_BLECORE_Broadcast_Information.jpg](images/0006_BLECORE_Broadcast_Information.jpg)
* 连接设备，查看Profile：  
  ![0006_BLECORE_Conect_And_Show_Profile.jpg](images/0006_BLECORE_Conect_And_Show_Profile.jpg)
* 获取、修改属性：  
  ![0006_BLECORE_Read_Write_Attribute.jpg](images/0006_BLECORE_Read_Write_Attribute.jpg)

# Simple GATT Profile Characteristic Table

* BTool Show:  
  ![0006_Simple_GATT_Profile_Characteristic_Table_from_BTool.png](images/0006_Simple_GATT_Profile_Characteristic_Table_from_BTool.png)
* BLECORE Show:  
  ![0006_BLECORE_Simple_GATT_Profile_Characteristic_Table.jpg](images/0006_BLECORE_Simple_GATT_Profile_Characteristic_Table.jpg)
