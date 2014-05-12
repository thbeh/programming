package main

import (
    "fmt"
/*    "os"
    "bufio"
*/
    "strings"
    "github.com/huin/goserial"
    "github.com/thbeh/lcdgo"
    "time"
    "syscall"
    "net"
    "strconv"
)

var part = map[string]string {
        "root": "/",
        "home": "/home",
}

func FloatToString(input_num float64) string {
	return strconv.FormatFloat(input_num, 'f', 0, 64)
}

func main() {
    c := &goserial.Config{Name: "/dev/ttyACM0", Baud: 9600}
    s, _ := goserial.OpenPort(c)
    time.Sleep(1 * time.Second)

    b := make([]byte,12)
    
    for {
    	n, err := s.Read(b)
    	if err != nil {
	    fmt.Println(err)
    	}
	switch {
	    case string(b[:n]) == "1":
		lines, er := lcdgo.Get_lsb_information("/etc/lsb-release")
		if er != nil {
		   fmt.Println(er)
		}
		line := lines["DISTRIB_DESCRIPTION"]
		line = strings.Trim(line,"\x22")
	        var n syscall.Utsname
		_ = syscall.Uname(&n)
		l := lcdgo.CharsToString(n.Release)
		line = line+"~"+l
    	        fmt.Println(line)
        	_, err = s.Write([]byte(line))
        	if err != nil {
                   fmt.Println(err)
        	}
	    case string(b[:n]) == "2":
		line := ""
		ifs, er := net.Interfaces()
		if er != nil {
		   fmt.Print(er)
		}
		for _, v := range ifs {
		   addrs, _ := v.Addrs(); if len(addrs) == 0 {
			continue
		   }
		   if v.Name == "lo" {
			continue
		   }
		   ni := v.Name[:1]+v.Name[len(v.Name)-1:]
		   line = line + ni+"#"+addrs[0].String()+"~"
		}
		fmt.Println(line)
        	_, err = s.Write([]byte(line))
        	if err != nil {
                   fmt.Println(err)
        	}
	    case string(b[:n]) == "3":
		stat:= ""
		for _, value := range part {
		   du := lcdgo.DiskUsage(value)
                   percent := (du.Used / du.All) * 100
                   balance := FloatToString((100.0 - percent)/4)
                   stat = stat+fmt.Sprintf("%-6s",value)+fmt.Sprintf("%4.0f", du.All)+"G"+"#"+balance+"~"
		}
/*
		home := "/"
		du := lcdgo.DiskUsage(home)
		percent := (du.Used / du.All) * 100
		balance := RoundFloat((100 - percent)/4, 3)
		stat := "~"+fmt.Sprintf("%-6s",home)+fmt.Sprintf("%4.0f", du.All)+"G"+"#"+fmt.Sprintf("%3.1f",balance)		
*/
		fmt.Println(stat)
        	_, err = s.Write([]byte(stat))
        	if err != nil {
                   fmt.Println(err)
        	}
    	}
    }
/* 
    bio := bufio.NewReader(os.Stdin)
    for {
    	line, err:= bio.ReadString('\n')
    	if err != nil {
	    fmt.Println(err)
    	}	
	line = strings.Trim(line,"\n")
        if line == "exit" {
	    break
	}
        _, err = s.Write([]byte(line))
        if err != nil {
	    fmt.Println(err)
        }
    	fmt.Println(line) 
    }
*/

}
