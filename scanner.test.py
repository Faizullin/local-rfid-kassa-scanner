from src.uhfRfidScanner import UhdRfidScanner

uhdRfidScanner = UhdRfidScanner()
uhdRfidScanner.test = False
uhdRfidScanner.record = True
uhdRfidScanner.on()
uhdRfidScanner.connect()
uhdRfidScanner.run()