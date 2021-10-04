; Auto-generated. Do not edit!


(cl:in-package deu_ros-msg)


;//! \htmlinclude Complex.msg.html

(cl:defclass <Complex> (roslisp-msg-protocol:ros-message)
  ((real
    :reader real
    :initarg :real
    :type cl:float
    :initform 0.0)
   (imaginary
    :reader imaginary
    :initarg :imaginary
    :type cl:float
    :initform 0.0))
)

(cl:defclass Complex (<Complex>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <Complex>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'Complex)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name deu_ros-msg:<Complex> is deprecated: use deu_ros-msg:Complex instead.")))

(cl:ensure-generic-function 'real-val :lambda-list '(m))
(cl:defmethod real-val ((m <Complex>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader deu_ros-msg:real-val is deprecated.  Use deu_ros-msg:real instead.")
  (real m))

(cl:ensure-generic-function 'imaginary-val :lambda-list '(m))
(cl:defmethod imaginary-val ((m <Complex>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader deu_ros-msg:imaginary-val is deprecated.  Use deu_ros-msg:imaginary instead.")
  (imaginary m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <Complex>) ostream)
  "Serializes a message object of type '<Complex>"
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'real))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'imaginary))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <Complex>) istream)
  "Deserializes a message object of type '<Complex>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'real) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'imaginary) (roslisp-utils:decode-single-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<Complex>)))
  "Returns string type for a message object of type '<Complex>"
  "deu_ros/Complex")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Complex)))
  "Returns string type for a message object of type 'Complex"
  "deu_ros/Complex")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<Complex>)))
  "Returns md5sum for a message object of type '<Complex>"
  "54da470dccf15d60bd273ab751e1c0a1")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'Complex)))
  "Returns md5sum for a message object of type 'Complex"
  "54da470dccf15d60bd273ab751e1c0a1")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<Complex>)))
  "Returns full string definition for message of type '<Complex>"
  (cl:format cl:nil "float32 real~%float32 imaginary~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'Complex)))
  "Returns full string definition for message of type 'Complex"
  (cl:format cl:nil "float32 real~%float32 imaginary~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <Complex>))
  (cl:+ 0
     4
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <Complex>))
  "Converts a ROS message object to a list"
  (cl:list 'Complex
    (cl:cons ':real (real msg))
    (cl:cons ':imaginary (imaginary msg))
))
