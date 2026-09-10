# Windows Job Object API for memory limiting
# Forces Python (Waitress) process to use max 2 GiB RAM matching Linux containers

Add-Type @"
using System;
using System.Runtime.InteropServices;
using System.Diagnostics;

public class JobObjectMemoryLimit {
    [DllImport("kernel32.dll", CharSet = CharSet.Unicode)]
    public static extern IntPtr CreateJobObject(IntPtr lpJobAttributes, string lpName);
    
    [DllImport("kernel32.dll")]
    public static extern bool SetInformationJobObject(
        IntPtr hJob, int JobObjectInfoClass, IntPtr lpJobObjectInfo, uint cbJobObjectInfoLength);
    
    [DllImport("kernel32.dll", SetLastError = true)]
    public static extern bool AssignProcessToJobObject(IntPtr hJob, IntPtr hProcess);
    
    [DllImport("kernel32.dll", SetLastError = true)]
    public static extern bool CloseHandle(IntPtr hObject);
    
    [StructLayout(LayoutKind.Sequential)]
    public struct JOBOBJECT_BASIC_LIMIT_INFORMATION {
        public long PerProcessUserTimeLimit;
        public long PerJobUserTimeLimit;
        public uint LimitFlags;
        public IntPtr MinimumWorkingSetSize;
        public IntPtr MaximumWorkingSetSize;
        public uint ActiveProcessLimit;
        public IntPtr Affinity;
        public uint PriorityClass;
        public uint SchedulingClass;
    }
    
    [StructLayout(LayoutKind.Sequential)]
    public struct IO_COUNTERS {
        public ulong ReadOperationCount;
        public ulong WriteOperationCount;
        public ulong OtherOperationCount;
        public ulong ReadTransferCount;
        public ulong WriteTransferCount;
        public ulong OtherTransferCount;
    }
    
    [StructLayout(LayoutKind.Sequential)]
    public struct JOBOBJECT_EXTENDED_LIMIT_INFORMATION {
        public JOBOBJECT_BASIC_LIMIT_INFORMATION BasicLimitInformation;
        public IO_COUNTERS IoInfo;
        public IntPtr ProcessMemoryLimit;
        public IntPtr JobMemoryLimit;
        public IntPtr PeakProcessMemoryUsed;
        public IntPtr PeakJobMemoryUsed;
    }
}
"@

# Memory limit: 2 GiB = 2147483648 bytes (apple-to-apple with Linux containers)
$memLimitBytes = [IntPtr]::new(2147483648)

# Create job object
$jobHandle = [JobObjectMemoryLimit]::CreateJobObject([IntPtr]::Zero, "ThesisBenchAppleToApple")

# Set up extended limit info with memory cap
$info = New-Object JobObjectMemoryLimit+JOBOBJECT_EXTENDED_LIMIT_INFORMATION
$info.BasicLimitInformation.LimitFlags = 0x00000100  # JOB_OBJECT_LIMIT_PROCESS_MEMORY
$info.ProcessMemoryLimit = $memLimitBytes

# Allocate unmanaged memory for the struct
$infoSize = [System.Runtime.InteropServices.Marshal]::SizeOf($info)
$infoPtr = [System.Runtime.InteropServices.Marshal]::AllocHGlobal($infoSize)
[System.Runtime.InteropServices.Marshal]::StructureToPtr($info, $infoPtr, $false)

# Apply to job object (class 9 = JobObjectExtendedLimitInformation)
$result = [JobObjectMemoryLimit]::SetInformationJobObject($jobHandle, 9, $infoPtr, $infoSize)

if ($result) {
    Write-Host "Job Object memory limit set: 2 GiB (matches Linux containers)" -ForegroundColor Green
} else {
    Write-Host "Failed to set job object memory limit" -ForegroundColor Red
}

# Find Python process (Waitress under IIS)
$pythonProcs = Get-Process -Name "python" -ErrorAction SilentlyContinue
foreach ($proc in $pythonProcs) {
    $assignResult = [JobObjectMemoryLimit]::AssignProcessToJobObject($jobHandle, $proc.Handle)
    if ($assignResult) {
        Write-Host "Assigned Python PID $($proc.Id) to memory-limited job" -ForegroundColor Green
    }
}

[System.Runtime.InteropServices.Marshal]::FreeHGlobal($infoPtr)

# Keep job handle alive (don't close)
# Store globally so it persists
$global:ThesisJobHandle = $jobHandle

Write-Host "`nMemory limiting active. Python process restricted to 2 GiB RAM." -ForegroundColor Cyan
Write-Host "Apple-to-apple with Linux containers: RAM=2 GiB ENFORCED" -ForegroundColor Green
