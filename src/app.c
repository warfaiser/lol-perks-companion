#define _WIN32_WINNT 0x0601
#include <windows.h>
#include <shellapi.h>
#include <shlobj.h>
#include <stdio.h>
#include <stdlib.h>

extern const unsigned char embedded_html[];
extern const unsigned int embedded_html_len;

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    char targetFolder[MAX_PATH];
    char targetPath[MAX_PATH];

    // Method 1: Try SHGetFolderPath to get CSIDL_LOCAL_APPDATA
    HRESULT hr = SHGetFolderPathA(NULL, CSIDL_LOCAL_APPDATA, NULL, 0, targetFolder);
    if (FAILED(hr)) {
        // Fallback to Temp
        DWORD len = GetTempPathA(MAX_PATH, targetFolder);
        if (len == 0 || len > MAX_PATH) {
            GetCurrentDirectoryA(MAX_PATH, targetFolder);
        }
    }

    // Append folder name
    char appDir[MAX_PATH];
    snprintf(appDir, sizeof(appDir), "%s\\LoLPerksApp", targetFolder);
    CreateDirectoryA(appDir, NULL);

    snprintf(targetPath, sizeof(targetPath), "%s\\index.html", appDir);

    // Write the embedded standalone HTML
    FILE *f = fopen(targetPath, "wb");
    if (!f) {
        // Fallback to current folder
        GetCurrentDirectoryA(MAX_PATH, targetFolder);
        snprintf(targetPath, sizeof(targetPath), "%s\\LoLPerksApp.html", targetFolder);
        f = fopen(targetPath, "wb");
    }

    if (f) {
        fwrite(embedded_html, 1, embedded_html_len, f);
        fclose(f);
    }

    // Try opening as standalone Edge App window if Edge exists
    char edgeCmd[1024];
    const char *edgeLocations[] = {
        "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
        "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe",
        NULL
    };

    int launched = 0;
    for (int i = 0; edgeLocations[i] != NULL; i++) {
        DWORD dw = GetFileAttributesA(edgeLocations[i]);
        if (dw != INVALID_FILE_ATTRIBUTES && !(dw & FILE_ATTRIBUTE_DIRECTORY)) {
            // Note: pass normal Windows file path in quotes, not file:///
            snprintf(edgeCmd, sizeof(edgeCmd), "\"%s\" --app=\"%s\"", edgeLocations[i], targetPath);
            STARTUPINFOA si;
            PROCESS_INFORMATION pi;
            ZeroMemory(&si, sizeof(si));
            si.cb = sizeof(si);
            ZeroMemory(&pi, sizeof(pi));

            if (CreateProcessA(NULL, edgeCmd, NULL, NULL, FALSE, 0, NULL, NULL, &si, &pi)) {
                CloseHandle(pi.hProcess);
                CloseHandle(pi.hThread);
                launched = 1;
                break;
            }
        }
    }

    // If Edge App failed or not found, open with default browser via standard ShellExecute
    if (!launched) {
        HINSTANCE hRes = ShellExecuteA(NULL, "open", targetPath, NULL, NULL, SW_SHOWNORMAL);
        if ((INT_PTR)hRes <= 32) {
            // Fallback to cmd
            char cmd[MAX_PATH * 2];
            snprintf(cmd, sizeof(cmd), "cmd.exe /c start \"\" \"%s\"", targetPath);
            WinExec(cmd, SW_HIDE);
        }
    }

    return 0;
}
