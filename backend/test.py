import tensorflow as tf
import sys
image_path = sys.argv[1]
graph_file = "Venomous_nonVenomous_inception.pb"
labels_txt = "snake_labels.txt"
with tf.gfile.FastGFile(graph_file, 'rb') as f:
	graph_def = tf.GraphDef()
	graph_def.ParseFromString(f.read())
	_ = tf.import_graph_def(graph_def, name='')
image_data = tf.gfile.FastGFile(image_path, 'rb').read()
label_lines = [line.rstrip() for line in tf.gfile.GFile(labels_txt)]


with tf.Session() as sess:
	softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
	predictions = sess.run(softmax_tensor,{'DecodeJpeg/contents:0': image_data})
	top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
	temp = ['','']
	for node_id in top_k:
		human_string = label_lines[node_id]
		score = predictions[0][node_id]
		print('%s (score = %.5f)' % (human_string, score))