****************************************************
* 01_environment_and_manual_checks.do
* Check Stata version, packages, and command help.
****************************************************

about
which xtset
which xtreg
which regress
which areg
which poisson
which nbreg
which fracreg
which margins
which marginsplot
which lincom
which nlcom
which bootstrap
which testnl

* Optional/community commands: run only if approved in checkpoint C1.
local optional_cmds "reghdfe ftools ppmlhdfe boottest esttab"
foreach cmd of local optional_cmds {
    di as text "Checking optional command: `cmd'"
    capture which `cmd'
    if _rc {
        di as error "Optional command `cmd' is not installed. Do not use unless user approves installation or fallback."
    }
    else {
        di as result "Optional command `cmd' found."
    }
}

* Retrieve installed help locally if needed.
* help xtreg
* help margins
* help fracreg
