pragma solidity ^0.5.8;

contract DocMed
{
    struct Doctor
    {
        address wallet;
        uint doctorNPWZ;
        string name;
        string lastName;
    }
    
    struct Visit
    {
        address doctor;
        uint timestamp;
        string doctorRecommendations;
    }
    
    struct HospitalResidance
    {
        uint visitsNo;
        mapping(uint => Visit) visits;
    }
    
    struct Patient
    {
        address wallet;
        string pesel;
        string name;
        string lastName;
        int residancesNo;
        HospitalResidance[] residances;
        bool inHospital;
    }
    
    address[] public doctorIds;
    mapping(address => Doctor) public doctors;
    address[] public patientIds;
    mapping(address => Patient) public patients;
    address adminWallet;
    
    constructor() public
    {
        adminWallet = msg.sender;
    }
    
    function patientExists(address _patient) view internal returns(bool)
    {
        return patients[_patient].wallet == _patient;
    }
    
    function doctorExists(address _doctor) view internal returns(bool)
    {
        return doctors[_doctor].wallet == _doctor;
    }
    
    function registerPatient(string memory _pesel, string memory _name, string memory _lastName) public
    {
        require(!patientExists(msg.sender));
        Patient storage p = patients[msg.sender];
        p.wallet = msg.sender;
        p.pesel = _pesel;
        p.name = _name;
        p.lastName = _lastName;
        patientIds.push(msg.sender);
    }
    
    function registerDoctor(address _wallet, uint _npwz, string memory _name, string memory _lastName) public
    {
        require(msg.sender == adminWallet);
        require(!doctorExists(_wallet));
        Doctor storage d = doctors[_wallet];
        d.wallet = _wallet;
        d.doctorNPWZ = _npwz;
        d.name = _name;
        d.lastName = _lastName;
        doctorIds.push(_wallet);
    }
    
    function addResidanceInternal(Patient storage _p) internal
    {
        _p.inHospital = true;
        _p.residancesNo += 1;
        HospitalResidance memory hr;
        hr.visitsNo = 0;
        _p.residances.push(hr);
    }
    
    function addResidance(address _patient) external
    {
        require(patientExists(_patient));
        Patient storage p = patients[_patient];
        require(!p.inHospital);
        addResidanceInternal(p);
    }
    
    function addVisit(address _patient, string memory _recommendations) public
    {
        require(doctorExists(msg.sender));
        require(patientExists(_patient));
        Patient storage p = patients[_patient];
        if(!p.inHospital)
            addResidanceInternal(p);
        HospitalResidance storage hr = p.residances[uint(p.residancesNo - 1)];
        Visit storage v = hr.visits[hr.visitsNo];
        hr.visitsNo += 1;
        v.doctor = msg.sender;
        v.timestamp = now;
        v.doctorRecommendations = _recommendations;
    }
    
    function getDoctorsNo() public view returns(uint)
    {
        return doctorIds.length;
    }
    
    function getPatientsNo() public view returns(uint)
    {
        return patientIds.length;
    }
}
