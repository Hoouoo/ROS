// Auto-generated. Do not edit!

// (in-package deu_ros.srv)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------


//-----------------------------------------------------------

class WordCountRequest {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.words = null;
    }
    else {
      if (initObj.hasOwnProperty('words')) {
        this.words = initObj.words
      }
      else {
        this.words = '';
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type WordCountRequest
    // Serialize message field [words]
    bufferOffset = _serializer.string(obj.words, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type WordCountRequest
    let len;
    let data = new WordCountRequest(null);
    // Deserialize message field [words]
    data.words = _deserializer.string(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += object.words.length;
    return length + 4;
  }

  static datatype() {
    // Returns string type for a service object
    return 'deu_ros/WordCountRequest';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '6f897d3845272d18053a750c1cfb862a';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    string words
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new WordCountRequest(null);
    if (msg.words !== undefined) {
      resolved.words = msg.words;
    }
    else {
      resolved.words = ''
    }

    return resolved;
    }
};

class WordCountResponse {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.count = null;
    }
    else {
      if (initObj.hasOwnProperty('count')) {
        this.count = initObj.count
      }
      else {
        this.count = 0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type WordCountResponse
    // Serialize message field [count]
    bufferOffset = _serializer.uint32(obj.count, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type WordCountResponse
    let len;
    let data = new WordCountResponse(null);
    // Deserialize message field [count]
    data.count = _deserializer.uint32(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 4;
  }

  static datatype() {
    // Returns string type for a service object
    return 'deu_ros/WordCountResponse';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'ac8b22eb02c1f433e0a55ee9aac59a18';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    uint32 count
    
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new WordCountResponse(null);
    if (msg.count !== undefined) {
      resolved.count = msg.count;
    }
    else {
      resolved.count = 0
    }

    return resolved;
    }
};

module.exports = {
  Request: WordCountRequest,
  Response: WordCountResponse,
  md5sum() { return '58903d21a3264f3408d79ba79e9f7c7e'; },
  datatype() { return 'deu_ros/WordCount'; }
};
