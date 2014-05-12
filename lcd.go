package lcdgo

import ( 
	"fmt"
	"syscall"
	"os"
	"bufio"
	"strings"
	"errors"
)

type PyString string
type Utsname syscall.Utsname
type DiskStatus struct {
	All	float64 `json:"all"`
	Used	float64 `json:"used"`
	Free	float64 `json:"free"`
}

func (py PyString) Split(str string) (string, string, error) {
    s := strings.Split(string(py), str)
    if len(s) > 2 {
	return "", "", errors.New("Minimum match not found")
    }
    return s[0], s[1], nil
}

func Get_lsb_information(path string) (map[string]string, error) {
    file, err := os.Open(path)
    if err != nil {
	return nil, err
    }
    defer file.Close()
    var py PyString
    var splits = map[string]string{}
    scanner := bufio.NewScanner(file)
    for scanner.Scan() {
	py = PyString(scanner.Text())
	arg, value, err := py.Split("=")
	if err != nil {
		fmt.Println(err)
	}
/*        s := strings.Split(scanner.Text(),"=") */
/*	arg, value := s[0], s[1] */
	splits[arg] =  value
    }
    return splits, scanner.Err()
}

func uname() (*syscall.Utsname, error) {
    uts := &syscall.Utsname{}
    if err := syscall.Uname(uts); err != nil {
	return nil, err
    }
    return uts, nil
}

func DiskUsage(path string) (disk DiskStatus) {
    fs := syscall.Statfs_t{}
    err := syscall.Statfs(path, &fs)
    if err != nil {
	return
    }
    disk.All = float64((fs.Blocks * uint64(fs.Bsize)) / 1073741824)
    disk.Free = float64((fs.Bfree * uint64(fs.Bsize)) / 1073741824)
    disk.Used = disk.All - disk.Free
    return
}

func CharsToString(ca [65]int8) string {
    s := make([]byte, len(ca))
    var lens int
    for ; lens < len(ca); lens++ {
	if ca[lens] == 0 {
	     break
	}
	s[lens] = uint8(ca[lens])
    }
    return string(s[0:lens])
}

