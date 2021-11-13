;; Auto-generated. Do not edit!


(when (boundp 'deu_ros::WordCount)
  (if (not (find-package "DEU_ROS"))
    (make-package "DEU_ROS"))
  (shadow 'WordCount (find-package "DEU_ROS")))
(unless (find-package "DEU_ROS::WORDCOUNT")
  (make-package "DEU_ROS::WORDCOUNT"))
(unless (find-package "DEU_ROS::WORDCOUNTREQUEST")
  (make-package "DEU_ROS::WORDCOUNTREQUEST"))
(unless (find-package "DEU_ROS::WORDCOUNTRESPONSE")
  (make-package "DEU_ROS::WORDCOUNTRESPONSE"))

(in-package "ROS")





(defclass deu_ros::WordCountRequest
  :super ros::object
  :slots (_words ))

(defmethod deu_ros::WordCountRequest
  (:init
   (&key
    ((:words __words) "")
    )
   (send-super :init)
   (setq _words (string __words))
   self)
  (:words
   (&optional __words)
   (if __words (setq _words __words)) _words)
  (:serialization-length
   ()
   (+
    ;; string _words
    4 (length _words)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _words
       (write-long (length _words) s) (princ _words s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _words
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _words (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(defclass deu_ros::WordCountResponse
  :super ros::object
  :slots (_count ))

(defmethod deu_ros::WordCountResponse
  (:init
   (&key
    ((:count __count) 0)
    )
   (send-super :init)
   (setq _count (round __count))
   self)
  (:count
   (&optional __count)
   (if __count (setq _count __count)) _count)
  (:serialization-length
   ()
   (+
    ;; uint32 _count
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; uint32 _count
       (write-long _count s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint32 _count
     (setq _count (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;;
   self)
  )

(defclass deu_ros::WordCount
  :super ros::object
  :slots ())

(setf (get deu_ros::WordCount :md5sum-) "58903d21a3264f3408d79ba79e9f7c7e")
(setf (get deu_ros::WordCount :datatype-) "deu_ros/WordCount")
(setf (get deu_ros::WordCount :request) deu_ros::WordCountRequest)
(setf (get deu_ros::WordCount :response) deu_ros::WordCountResponse)

(defmethod deu_ros::WordCountRequest
  (:response () (instance deu_ros::WordCountResponse :init)))

(setf (get deu_ros::WordCountRequest :md5sum-) "58903d21a3264f3408d79ba79e9f7c7e")
(setf (get deu_ros::WordCountRequest :datatype-) "deu_ros/WordCountRequest")
(setf (get deu_ros::WordCountRequest :definition-)
      "string words
---
uint32 count

")

(setf (get deu_ros::WordCountResponse :md5sum-) "58903d21a3264f3408d79ba79e9f7c7e")
(setf (get deu_ros::WordCountResponse :datatype-) "deu_ros/WordCountResponse")
(setf (get deu_ros::WordCountResponse :definition-)
      "string words
---
uint32 count

")



(provide :deu_ros/WordCount "58903d21a3264f3408d79ba79e9f7c7e")


