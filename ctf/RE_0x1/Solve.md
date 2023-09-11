### Howdy,

### Welcome to the writeup for **"Keygen"** - a CTF challenge that will mainly test your Network analysis skills (little bit of searching too).
Let's dive in.

##

### Simple Inspection

Firstly, the archive name is "RE_0x1.zip". (that was just for distracting😛)

The archive contains a **notes.txt** & 2 stripped go binaries (meaning its debugging information were removed)

```
challenge: ELF 64-bit LSB pie executable, x86-64,
challenge.exe: PE32+ executable (console) x86-64 for MS Windows
```

Let's Run the Binary. (I am using my windows machine)

![1](https://user-images.githubusercontent.com/56682134/258880567-198667cb-d8f6-4d3b-bd23-08b120a18960.png)

In the binary there is a ASCII logo named "Keygen" & a probable hint "Network is Bliss" printed.
After entering something the file was closing automatically. So, I run the exe in windows cmd to see the printed message.
It was printing "Auth Failed"

![2](https://user-images.githubusercontent.com/56682134/258880627-76246948-ceaa-461e-b54b-8b80cef73287.png)

Now lets see the "notes.txt"  as the description of the challenge described that **"Every hint is important."**

![3](https://user-images.githubusercontent.com/56682134/258880647-86869290-d133-4796-816a-ea78139e2514.png)

In the note there was again the text **"Network is Bliss"** & a new one **"Things will be great when you’re… downtown!"**
> If you have watched Netflix’s *‘Red Notice’*, its an Bishop (Gal Gadot) reference. Any way that's not the point.

The hint indicates us to **go down** & the text file was quite long. At the end there were some python codes & possible hints.

![4](https://user-images.githubusercontent.com/56682134/258880666-c992afdc-0622-4f5d-a3b7-1b98ac302801.png)


If you look at the Python code snippet:
- It first checks the operating system of the machine. If it's a Windows system, it gets the UUID (unique identifier) of the computer. If it's not, then it uses the `uname -a` command to get system information.
- Then it encodes the value & replaces some values & add random 7 digits before & after that.
- It checks if the resulting string is in a database (presumably, `check_DB(user_id)` is a function that checks a database for a given user ID).
- If the string is in the database, it prints "Bingo???" **Possibly the flag**.
- Then after waiting 69 seconds it prints **"Don't Forget to remove raw"**. The string 'raw' is reversed using slicing.

- One more thing. there was a comment **I think, we need a better name for blackhole**. Meaning "blackhole" is some kind of thing & We need to rename it. (*It may seem guessy to some people*)

That's almost everything about the challenge description & provided hints.

##

### Reversing the binary

- First let's use strings to see if there was any flag there. I tried using the regex `'.{4}(?=\{)[^}\s]*}'` for capturing any word within the curly braces & found a **caeser ciphertext** with shift 6. Which is actually a Fake Flag.

  ![5](https://user-images.githubusercontent.com/56682134/258881203-f24da5a3-8ab6-4d83-bac8-93add7e175fa.png)
  ![6](https://user-images.githubusercontent.com/56682134/258881220-7fdf1036-3555-4e9d-9ae8-2fa839de7396.png)

- Although it was a stripped binary I tried to understand the code. But I found nothing except the file was using some go modules like `strings`, `runtime`, `encoding/base64`, `encoding/hex`, `unicode`, `encoding/json`, `syscall` & `net/http`

- While running `strings` there were some custom module usage
```
challenge/process.Processes
challenge/process.(*UnixProcess).Executable
challenge/process.processes
challenge/process.processes.func1
challenge/process.newUnixProcess
challenge/process.(*UnixProcess).Refresh
```
- After some searching I found out that it can be some code similar to the go module `go-ps` (which is used for inspecting processes in golang).

  ![7](https://user-images.githubusercontent.com/56682134/258881274-6abccc2f-b0dc-4ab6-ae32-6ca90064fe4a.png)

- While the script was using `net/http` module & the python code snippet hinted it was comparing the data using a function & the main part, the text **"Networking is Bliss"**, It was pretty obvious that was a hint to check the network flow. (Not guessy. Even ChatGPT responded the same)

##

### Renaming is the Key

- So, **Burpsuite** is the first software that come in our mind for capturing/analyzing network traffic. But when we run "Burpsuite" the script was exiting automatically printing the message **"[!] Hey! burp is in the blackhole!"**.

  ![9](https://user-images.githubusercontent.com/56682134/258881304-24a2de1e-5954-4634-90e6-884543a7631c.png)

- Same thing appeared for multiple software's running (Wireshark, Ghidra, x64dbg, Charles Proxy). So, its pretty obvious that the script is analyzing the process running & exiting if the software is in some kind of "Blacklist" / "Blackhole".

- After searching in Github for **golang "Anti Debugger"** there was a repository named "buggi". In the readme there was a line

  ![8](https://user-images.githubusercontent.com/56682134/258881332-b38aec2a-012d-44a4-ada5-a1d3d7082455.png)

- Which matches with our hint
  > **I think, we need a better name for blackhole.**

- So, lets change our **burpsuite** name to something else. But the error was still there.. The challenge script might have some other functionality there.

  ![10](https://user-images.githubusercontent.com/56682134/258881550-023e7cea-72e0-4339-8824-aa64a81543f7.png)

- So, lets remove the word "burpsuite" form the entire command (even the folder name. most tricky part i think).

  ![11](https://user-images.githubusercontent.com/56682134/258881569-348f788d-c39f-4cea-a730-484217d64583.png)

- Bingo, Now the script is still running.

  ![12](https://user-images.githubusercontent.com/56682134/258881613-393dcee8-fa93-40b8-8d2d-d881aa46d293.png)

##

### CTF: Capturing the Traffic!!

- To capture traffic from a go binary using **Burp Proxy** we have to set an **environment variable**

  - For windows cmd:
  ```
  set https_proxy=127.0.0.1:8080
  ```
  - For linux system:
  ```
  export https_proxy=127.0.0.1:8080
  ```
- After configuring the proxy & running the file we see a request popping in the burp proxy interceptor. Its a **gist url**!!!

  ![13](https://user-images.githubusercontent.com/56682134/258881961-cc490835-b836-4e2d-8d31-6625473dce7f.png)

- In the gist url there were some encoded texts under the name "admin", "69". Most probably those were the comparable texts in the `CheckDB()` function.

  ![14](https://user-images.githubusercontent.com/56682134/258882246-c059ff1f-7b95-4add-816c-7de6a895e93b.png)

- Lets generate out own ID using the provided "python snippet". You need some basic python knowledge for that.

  ![15](https://user-images.githubusercontent.com/56682134/258882272-651face3-0fb4-4a37-b727-f3747755920d.png)

- Lets intercept the data transmitted from the binary & replace with our own "ID" in burp proxy.

  ![16](https://user-images.githubusercontent.com/56682134/258882298-8e0606aa-d987-4653-8208-6d53515a566b.png)
  ![17](https://user-images.githubusercontent.com/56682134/258882320-8b25a14e-a56d-4ebb-b624-79b5054d2df3.png)

- After doing it correctly, the script now prints "Authorized" but it prints the fake flag we got after running `strings`.

  ![18](https://user-images.githubusercontent.com/56682134/258882584-a6444af5-9deb-430a-85d6-30b9c1a67e40.png)

So,,,,,,,

##

##### Where's the Flag??

- Remember the **notes.txt**?? There was a line at the end of the python code snippet.
  > **Don't Forget to remove raw**

- The gist url was in the format "gist.github.com/user/uniqueid/raw"

  ![19](https://user-images.githubusercontent.com/56682134/258883129-ac0acdb9-13fd-42d0-85ce-80be34e4b45a.png)

- Let's remove the `/raw` part & see what's there. Nothing special there except the **revisions**

  ![20](https://user-images.githubusercontent.com/56682134/258883251-a1dba1e7-214a-4763-9b7d-56d545230f2c.png)


- In the revisions theres our flag **"thbd{c0ngr4t5_r3n4m1ng_1s_Bl155}"**

  ![21](https://user-images.githubusercontent.com/56682134/258883149-78b1d698-2149-4560-a51a-110d2a2fea2e.png)

So, this was the solving process for the challenge. Though there were no solver, but I hope it was helpful for you in any way.

##### Scripts used :
- Process (go-ps fork): https://github.com/htr-tech/process
- ChatGPT for fixing the code. (Cause I am not familiar with golang that much)
- Challenge Files: Attached with the gist

**Special Thanks**: Mustakim Ahmed Sifat (**@bdhackers009**)
