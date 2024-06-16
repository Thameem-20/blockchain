// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ClinicalTrial {
    struct Trial {
        string id;
        string title;
        string description;
        string status;
        string sponsor;
        uint participants;
    }

    mapping(string => Trial) private trials;

    event TrialCreated(string id, string title, string description, string status, string sponsor, uint participants);
    event TrialUpdated(string id, string title, string description, string status, string sponsor, uint participants);
    event TrialDeleted(string id);

    function createTrial(string memory id, string memory title, string memory description, string memory status, string memory sponsor, uint participants) public {
        Trial memory newTrial = Trial({
            id: id,
            title: title,
            description: description,
            status: status,
            sponsor: sponsor,
            participants: participants
        });

        trials[id] = newTrial;
        emit TrialCreated(id, title, description, status, sponsor, participants);
    }

    function readTrial(string memory id) public view returns (string memory title, string memory description, string memory status, string memory sponsor, uint participants) {
        Trial memory trial = trials[id];
        return (trial.title, trial.description, trial.status, trial.sponsor, trial.participants);
    }

    function updateTrial(string memory id, string memory title, string memory description, string memory status, string memory sponsor, uint participants) public {
        Trial storage trial = trials[id];
        trial.title = title;
        trial.description = description;
        trial.status = status;
        trial.sponsor = sponsor;
        trial.participants = participants;

        emit TrialUpdated(id, title, description, status, sponsor, participants);
    }

    function deleteTrial(string memory id) public {
        delete trials[id];
        emit TrialDeleted(id);
    }
}
