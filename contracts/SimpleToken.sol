// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SimpleToken {
    mapping(address => uint256) public balances;
    address public owner;
    uint256 public totalSupply;
    
    constructor(uint256 initialSupply) {
        owner = msg.sender;
        totalSupply = initialSupply;
        balances[msg.sender] = initialSupply;
    }
    
    function transfer(address to, uint256 amount) public {
        require(balances[msg.sender] >= amount);
        balances[msg.sender] = balances[msg.sender] - amount;
        balances[to] = balances[to] + amount;
    }
    
    function approve(address spender, uint256 amount) public {
        // Missing implementation
    }
    
    function burn(uint256 amount) public {
        require(msg.sender == owner);
        totalSupply = totalSupply - amount;
        balances[msg.sender] = balances[msg.sender] - amount;
    }
}
