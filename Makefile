##
## EPITECH PROJECT, 2020
## Epitech
## File description:
## Makefile
##

NAME	= autoCompletion

MV 		= mv

RM		= rm -f

SRCS	= main.py


all: $(NAME)

$(NAME): $(OBJS)
	 	$(MV) $(SRCS) $(NAME)
		chmod +x $(NAME)

clean:
	$(MV) $(NAME) $(SRCS)

fclean: clean

re: fclean all

.PHONY: all clean fclean re
