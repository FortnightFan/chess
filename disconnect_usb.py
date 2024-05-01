import usb.core
import usb.util
import time

# Define vendor and product IDs of the target device
VENDOR_ID_TOP = 0x1234
PRODUCT_ID_TOP = 0x5678

VENDOR_ID_BOTTOM = 0x1234
PRODUCT_ID_BOTTOM = 0x5678
# Find the device
top_hub = usb.core.find(idVendor=VENDOR_ID_TOP, idProduct=PRODUCT_ID_TOP)
bottom_hub = usb.core.find(idVendor=VENDOR_ID_BOTTOM, idProduct=PRODUCT_ID_BOTTOM)

try:
    # Detach the device
    usb.util.dispose_resources(top_hub)    
    usb.util.dispose_resources(bottom_hub)
    print("Hubs detached.")
    
    time.sleep(1) 
    
    top_hub.set_configuration()
    usb.util.claim_interface(top_hub, 0)
    time.sleep(1) 
    bottom_hub.set_configuration()
    usb.util.claim_interface(bottom_hub, 0)

    print("Hubs reattached.")
    
except Exception as e:
    print("Error:", e)

finally:
    usb.util.dispose_resources(top_hub)
    usb.util.dispose_resources(bottom_hub)
