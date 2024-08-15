mesg = 'WEAREDISCOVEREDFLEEATONCE'

# def compare_char_counts(text1, text2):
#     from collections import defaultdict
#     text1_counts = defaultdict(int)
#     text2_counts = defaultdict(int)
#     for char in text1:
#         text1_counts[char] += 1
#     for char in text2:
#         text2_counts[char] += 1
#     for k in text1_counts.keys():
#         print '{}: {} - {}: {} - D: {}'.format(k, text1_counts[k], k, text2_counts[k], text1_counts[k] - text2_counts[k])

# def encode(msg, rails):
#     # step = cur_step = 2 * rails - 2
#     # encrypted_message = ''

#     # for i in range(rails - 1):
#     #     encrypted_message += msg[i::cur_step]
#     #     cur_step -= 2
#     # encrypted_message += msg[rails - 1::step]

#     # return encrypted_message

#     encmsg = ''
#     for r in range(rails):
#         for i in range(r, len(msg), rails):
#             encmsg += msg[i]
#     return encmsg

#     # cycle = 2 * rails - 2
#     # encmsg = ''
#     # subtract = True
#     # ld = {}
#     # #import pdb; pdb.set_trace()
#     # for c in range(len(msg) / cycle)
#     #     for i in range(rails):
#     #         n1 = (cycle * c) + i
#     #         if subtract:
#     #             n2 = cycle - (i * 2)
#     #             encmsg += msg[n1]
#     #             if not n1 == n2:
#     #                 encmsg += msg[n2]
#     #         else:
#     #             n2 = 

#     #     subtract = not subtract
#     # return encmsg





# def decode(msg, rails):
#     # step = cur_step = 2 * rails - 2
#     # decrypted_message = ''

#     # for i in range(rails - 1):
#     #     decrypted_message += msg[i::cur_step]
#     #     cur_step -= 2
#     # decrypted_message += msg[rails - 1::step]

#     # return decrypted_message
#     pass

# #######################################
# # dict[l1] = msg[0::2 * rails - 2] # 8
# # dict[l2] = msg[1::(2 * rails - 2) - 2] # 6
# # dict[l3] = msg[2::(2 * rails - 2) - 2 - 2 ] # 4
# # dict[l4] = msg[3::(2 * rails - 2) - 2 - 2 - 2 ] # 2
# # dict[l5] = msg[4::2 * rails - 2]

# # NVM just slice single characters from the initial string in the correct order
# #######################################

# print 'message'
# print mesg, 'len:', len(mesg)

# print '\nrail=3'
# enc = encode(mesg, 3)
# print enc, 'len:', len(enc)
# compare_char_counts(mesg, enc)

# print '\nrail=4'
# enc = encode(mesg, 4)
# print enc, 'len:', len(enc)
# compare_char_counts(mesg, enc)


from itertools import cycle


def rail_pattern(n):
    r = list(range(n))
    return cycle(r + r[-2:0:-1])


def encode(plaintext, rails):
    p = rail_pattern(rails)
    # this relies on key being called in order, guaranteed?
    return ''.join(sorted(plaintext, key=lambda i: next(p)))


#print encode(mesg, 3), ' - ', encode(mesg, 4)

c = 0

for x in rail_pattern(5):
    if c <= 25:
        print x
        c += 1
    else:
        break


def decode(ciphertext, rails):
    p = rail_pattern(rails)
    indexes = sorted(range(len(ciphertext)), key=lambda i: next(p))
    result = [''] * len(ciphertext)
    for i, c in zip(indexes, ciphertext):
        result[i] = c
    return ''.join(result)