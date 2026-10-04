CC = x86_64-w64-mingw32-gcc
WINDRES = x86_64-w64-mingw32-windres
CFLAGS = -mwindows -O2 -s -Wall

all: bin/LoL_Perks_App.exe

bin/resource.res: assets/resource.rc assets/app_icon.ico
	@mkdir -p bin
	$(WINDRES) assets/resource.rc -O coff -o bin/resource.res

bin/LoL_Perks_App.exe: src/app.c src/embedded_data.c bin/resource.res
	@mkdir -p bin
	$(CC) $(CFLAGS) src/app.c src/embedded_data.c bin/resource.res -o bin/LoL_Perks_App.exe
	@echo "Build complete: bin/LoL_Perks_App.exe"

clean:
	rm -f bin/*.res bin/*.exe

.PHONY: all clean
