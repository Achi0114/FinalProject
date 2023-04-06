// SPDX-License-Identifier: GPL-3.0
pragma experimental ABIEncoderV2;
pragma solidity ^0.8.18;

contract CovidPatients {
    address public owner = msg.sender;

    struct Patients {
        address ID;
        uint HN;
        string name;
    }
    mapping (address => Patients)  allPatients;

    struct VitalSign {
        address ID;
        uint HN;
        uint temp;
        uint hr;
        uint spo2;
        uint time;
    }
    mapping (address => VitalSign[])  vitalsign;

    function addPatient(address id, uint HN ,string memory name) public {
        Patients memory newPatients = Patients(id, HN, name);
        allPatients[id] = newPatients;
    }

    function getPatient(address id) public view returns(uint, string memory) {
        Patients memory c = allPatients[id];
        return (c.HN, c.name);    
    }

    function addVitalSign(address id, uint HN, uint temp, uint hr, uint spo2 ) public {
        VitalSign memory newVitalSign = VitalSign(id, HN, temp, hr, spo2, block.timestamp);
        vitalsign[id].push(newVitalSign);
    }


    function getVitalsign(address id) public view   returns(VitalSign[] memory)  {
        return vitalsign[id];    
    }
}

